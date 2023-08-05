import java.lang
import org.kie.api.runtime.rule
import org.optaplanner.core.api.score
import org.optaplanner.core.api.score.holder
import typing



class HardMediumSoftScore(org.optaplanner.core.api.score.AbstractScore['HardMediumSoftScore']):
    """
    public final class HardMediumSoftScore extends :class:`~org.optaplanner.core.api.score.AbstractScore`<:class:`~org.optaplanner.core.api.score.buildin.hardmediumsoft.HardMediumSoftScore`>
    
        This :class:`~org.optaplanner.core.api.score.Score` is based on 3 levels of int constraints: hard, medium and soft. Hard
        constraints have priority over medium constraints. Medium constraints have priority over soft constraints. Hard
        constraints determine feasibility.
    
        This class is immutable.
    
        Also see:
            :class:`~org.optaplanner.core.api.score.Score`, :meth:`~serialized`
    """
    ZERO: typing.ClassVar['HardMediumSoftScore'] = ...
    """
    public static final :class:`~org.optaplanner.core.api.score.buildin.hardmediumsoft.HardMediumSoftScore` ZERO
    
    
    """
    ONE_HARD: typing.ClassVar['HardMediumSoftScore'] = ...
    """
    public static final :class:`~org.optaplanner.core.api.score.buildin.hardmediumsoft.HardMediumSoftScore` ONE_HARD
    
    
    """
    ONE_MEDIUM: typing.ClassVar['HardMediumSoftScore'] = ...
    """
    public static final :class:`~org.optaplanner.core.api.score.buildin.hardmediumsoft.HardMediumSoftScore` ONE_MEDIUM
    
    
    """
    ONE_SOFT: typing.ClassVar['HardMediumSoftScore'] = ...
    """
    public static final :class:`~org.optaplanner.core.api.score.buildin.hardmediumsoft.HardMediumSoftScore` ONE_SOFT
    
    
    """
    def add(self, hardMediumSoftScore: 'HardMediumSoftScore') -> 'HardMediumSoftScore':
        """
            Description copied from interface: :meth:`~org.optaplanner.core.api.score.Score.add`
            Returns a Score whose value is (this + addend).
        
            Parameters:
                addend (:class:`~org.optaplanner.core.api.score.buildin.hardmediumsoft.HardMediumSoftScore`): value to be added to this Score
        
            Returns:
                this + addend
        
        
        """
        ...
    def compareTo(self, hardMediumSoftScore: 'HardMediumSoftScore') -> int: ...
    def divide(self, double: float) -> 'HardMediumSoftScore':
        """
            Description copied from interface: :meth:`~org.optaplanner.core.api.score.Score.divide`
            Returns a Score whose value is (this / divisor). When rounding is needed, it should be floored (as defined by
            :meth:`~org.optaplanner.core.api.score.buildin.hardmediumsoft.https:.docs.oracle.com.javase.8.docs.api.java.lang.Math.html?is`).
        
            If the implementation has a scale/precision, then the unspecified scale/precision of the double divisor should have no
            impact on the returned scale/precision.
        
            Parameters:
                divisor (double): value by which this Score is to be divided
        
            Returns:
                this / divisor
        
        
        """
        ...
    def equals(self, object: typing.Any) -> bool:
        """
        
            Overrides:
                
                meth:`~org.optaplanner.core.api.score.buildin.hardmediumsoft.https:.docs.oracle.com.javase.8.docs.api.java.lang.Object.html?is` in
                class :class:`~org.optaplanner.core.api.score.buildin.hardmediumsoft.https:.docs.oracle.com.javase.8.docs.api.java.lang.Object?is`
        
        
        """
        ...
    def getHardScore(self) -> int:
        """
            The total of the broken negative hard constraints and fulfilled positive hard constraints. Their weight is included in
            the total. The hard score is usually a negative number because most use cases only have negative constraints.
        
            Returns:
                higher is better, usually negative, 0 if no hard constraints are broken/fulfilled
        
        
        """
        ...
    def getMediumScore(self) -> int:
        """
            The total of the broken negative medium constraints and fulfilled positive medium constraints. Their weight is included
            in the total. The medium score is usually a negative number because most use cases only have negative constraints.
        
            In a normal score comparison, the medium score is irrelevant if the 2 scores don't have the same hard score.
        
            Returns:
                higher is better, usually negative, 0 if no medium constraints are broken/fulfilled
        
        
        """
        ...
    def getSoftScore(self) -> int:
        """
            The total of the broken negative soft constraints and fulfilled positive soft constraints. Their weight is included in
            the total. The soft score is usually a negative number because most use cases only have negative constraints.
        
            In a normal score comparison, the soft score is irrelevant if the 2 scores don't have the same hard and medium score.
        
            Returns:
                higher is better, usually negative, 0 if no soft constraints are broken/fulfilled
        
        
        """
        ...
    def hashCode(self) -> int:
        """
        
            Overrides:
                
                meth:`~org.optaplanner.core.api.score.buildin.hardmediumsoft.https:.docs.oracle.com.javase.8.docs.api.java.lang.Object.html?is` in
                class :class:`~org.optaplanner.core.api.score.buildin.hardmediumsoft.https:.docs.oracle.com.javase.8.docs.api.java.lang.Object?is`
        
        
        """
        ...
    def isFeasible(self) -> bool:
        """
            A :class:`~org.optaplanner.core.api.domain.solution.PlanningSolution` is feasible if it has no broken hard constraints.
        
            Returns:
                true if the :meth:`~org.optaplanner.core.api.score.buildin.hardmediumsoft.HardMediumSoftScore.getHardScore` is 0 or
                higher
        
        
        """
        ...
    def multiply(self, double: float) -> 'HardMediumSoftScore':
        """
            Description copied from interface: :meth:`~org.optaplanner.core.api.score.Score.multiply`
            Returns a Score whose value is (this * multiplicand). When rounding is needed, it should be floored (as defined by
            :meth:`~org.optaplanner.core.api.score.buildin.hardmediumsoft.https:.docs.oracle.com.javase.8.docs.api.java.lang.Math.html?is`).
        
            If the implementation has a scale/precision, then the unspecified scale/precision of the double multiplicand should have
            no impact on the returned scale/precision.
        
            Parameters:
                multiplicand (double): value to be multiplied by this Score.
        
            Returns:
                this * multiplicand
        
        
        """
        ...
    def negate(self) -> 'HardMediumSoftScore':
        """
            Description copied from interface: :meth:`~org.optaplanner.core.api.score.Score.negate`
            Returns a Score whose value is (- this).
        
            Returns:
                - this
        
        
        """
        ...
    @staticmethod
    def of(int: int, int2: int, int3: int) -> 'HardMediumSoftScore': ...
    @staticmethod
    def ofHard(int: int) -> 'HardMediumSoftScore': ...
    @staticmethod
    def ofMedium(int: int) -> 'HardMediumSoftScore': ...
    @staticmethod
    def ofSoft(int: int) -> 'HardMediumSoftScore': ...
    @staticmethod
    def ofUninitialized(int: int, int2: int, int3: int, int4: int) -> 'HardMediumSoftScore': ...
    @staticmethod
    def parseScore(string: str) -> 'HardMediumSoftScore': ...
    def power(self, double: float) -> 'HardMediumSoftScore':
        """
            Description copied from interface: :meth:`~org.optaplanner.core.api.score.Score.power`
            Returns a Score whose value is (this ^ exponent). When rounding is needed, it should be floored (as defined by
            :meth:`~org.optaplanner.core.api.score.buildin.hardmediumsoft.https:.docs.oracle.com.javase.8.docs.api.java.lang.Math.html?is`).
        
            If the implementation has a scale/precision, then the unspecified scale/precision of the double exponent should have no
            impact on the returned scale/precision.
        
            Parameters:
                exponent (double): value by which this Score is to be powered
        
            Returns:
                this ^ exponent
        
        
        """
        ...
    def subtract(self, hardMediumSoftScore: 'HardMediumSoftScore') -> 'HardMediumSoftScore':
        """
            Description copied from interface: :meth:`~org.optaplanner.core.api.score.Score.subtract`
            Returns a Score whose value is (this - subtrahend).
        
            Parameters:
                subtrahend (:class:`~org.optaplanner.core.api.score.buildin.hardmediumsoft.HardMediumSoftScore`): value to be subtracted from this Score
        
            Returns:
                this - subtrahend, rounded as necessary
        
        
        """
        ...
    def toLevelNumbers(self) -> typing.List[java.lang.Number]:
        """
            Description copied from interface: :meth:`~org.optaplanner.core.api.score.Score.toLevelNumbers`
            Returns an array of numbers representing the Score. Each number represents 1 score level. A greater score level uses a
            lower array index than a lesser score level.
        
            When rounding is needed, each rounding should be floored (as defined by
            :meth:`~org.optaplanner.core.api.score.buildin.hardmediumsoft.https:.docs.oracle.com.javase.8.docs.api.java.lang.Math.html?is`).
            The length of the returned array must be stable for a specific :class:`~org.optaplanner.core.api.score.Score`
            implementation.
        
            For example: :code:`-0hard/-7soft` returns :code:`new int{-0, -7}`
        
            The level numbers do not contain the :meth:`~org.optaplanner.core.api.score.Score.getInitScore`. For example:
            :code:`-3init/-0hard/-7soft` also returns :code:`new int{-0, -7}`
        
            Returns:
                never null
        
        
        """
        ...
    def toShortString(self) -> str:
        """
            Description copied from interface: :meth:`~org.optaplanner.core.api.score.Score.toShortString`
            Like
            :meth:`~org.optaplanner.core.api.score.buildin.hardmediumsoft.https:.docs.oracle.com.javase.8.docs.api.java.lang.Object.html?is`,
            but trims score levels which have a zero weight. For example 0hard/-258soft returns -258soft.
        
            Do not use this format to persist information as text, use
            :meth:`~org.optaplanner.core.api.score.buildin.hardmediumsoft.https:.docs.oracle.com.javase.8.docs.api.java.lang.Object.html?is`
            instead, so it can be parsed reliably.
        
            Returns:
                never null
        
        
        """
        ...
    def toString(self) -> str:
        """
        
            Overrides:
                
                meth:`~org.optaplanner.core.api.score.buildin.hardmediumsoft.https:.docs.oracle.com.javase.8.docs.api.java.lang.Object.html?is` in
                class :class:`~org.optaplanner.core.api.score.buildin.hardmediumsoft.https:.docs.oracle.com.javase.8.docs.api.java.lang.Object?is`
        
        
        """
        ...
    def withInitScore(self, int: int) -> 'HardMediumSoftScore':
        """
            Description copied from interface: :meth:`~org.optaplanner.core.api.score.Score.withInitScore`
            For example :code:`0hard/-8soft` with :code:`-7` returns :code:`-7init/0hard/-8soft`.
        
            Parameters:
                newInitScore (int): always negative (except in statistical calculations), 0 if all planning variables are initialized
        
            Returns:
                equals score except that :meth:`~org.optaplanner.core.api.score.Score.getInitScore` is set to :code:`newInitScore`
        
        
        """
        ...
    def zero(self) -> 'HardMediumSoftScore':
        """
            Description copied from interface: :meth:`~org.optaplanner.core.api.score.Score.zero`
            Returns a Score, all levels of which are zero.
        
            Returns:
                never null
        
        
        """
        ...

class HardMediumSoftScoreHolder(org.optaplanner.core.api.score.holder.ScoreHolder[HardMediumSoftScore]):
    """
    :class:`~org.optaplanner.core.api.score.buildin.hardmediumsoft.https:.docs.oracle.com.javase.8.docs.api.java.lang.Deprecated?is`(:meth:`~org.optaplanner.core.api.score.buildin.hardmediumsoft.https:.docs.oracle.com.javase.8.docs.api.java.lang.Deprecated.html?is`=true) public interface HardMediumSoftScoreHolder extends :class:`~org.optaplanner.core.api.score.holder.ScoreHolder`<:class:`~org.optaplanner.core.api.score.buildin.hardmediumsoft.HardMediumSoftScore`>
    
        Deprecated, for removal: This API element is subject to removal in a future version.
        Score DRL is deprecated and will be removed in a future major version of OptaPlanner. See
        :class:`~org.optaplanner.core.api.score.buildin.hardmediumsoft.https:.www.optaplanner.org.learn.drl`.
    
        Also see:
            :class:`~org.optaplanner.core.api.score.buildin.hardmediumsoft.HardMediumSoftScore`
    """
    def addHardConstraintMatch(self, ruleContext: org.kie.api.runtime.rule.RuleContext, int: int) -> None:
        """
            Deprecated, for removal: This API element is subject to removal in a future version.
        
            Parameters:
                kcontext (org.kie.api.runtime.rule.RuleContext): never null, the magic variable in DRL
                hardWeight (int): higher is better, negative for a penalty, positive for a reward
        
        
        """
        ...
    def addMediumConstraintMatch(self, ruleContext: org.kie.api.runtime.rule.RuleContext, int: int) -> None:
        """
            Deprecated, for removal: This API element is subject to removal in a future version.
        
            Parameters:
                kcontext (org.kie.api.runtime.rule.RuleContext): never null, the magic variable in DRL
                mediumWeight (int): higher is better, negative for a penalty, positive for a reward
        
        
        """
        ...
    def addMultiConstraintMatch(self, ruleContext: org.kie.api.runtime.rule.RuleContext, int: int, int2: int, int3: int) -> None:
        """
            Deprecated, for removal: This API element is subject to removal in a future version.
        
            Parameters:
                kcontext (org.kie.api.runtime.rule.RuleContext): never null, the magic variable in DRL
                hardWeight (int): higher is better, negative for a penalty, positive for a reward
                mediumWeight (int): higher is better, negative for a penalty, positive for a reward
                softWeight (int): higher is better, negative for a penalty, positive for a reward
        
        
        """
        ...
    def addSoftConstraintMatch(self, ruleContext: org.kie.api.runtime.rule.RuleContext, int: int) -> None:
        """
            Deprecated, for removal: This API element is subject to removal in a future version.
        
            Parameters:
                kcontext (org.kie.api.runtime.rule.RuleContext): never null, the magic variable in DRL
                softWeight (int): higher is better, negative for a penalty, positive for a reward
        
        
        """
        ...
    def impactScore(self, ruleContext: org.kie.api.runtime.rule.RuleContext, int: int) -> None:
        """
            Deprecated, for removal: This API element is subject to removal in a future version.
        
        """
        ...
    @typing.overload
    def penalize(self, ruleContext: org.kie.api.runtime.rule.RuleContext, int: int) -> None:
        """
            Deprecated, for removal: This API element is subject to removal in a future version.
            Penalize a match by the :class:`~org.optaplanner.core.api.domain.constraintweight.ConstraintWeight` negated and
            multiplied with the weightMultiplier for all score levels.
        
            Parameters:
                kcontext (org.kie.api.runtime.rule.RuleContext): never null, the magic variable in DRL
                weightMultiplier (int): at least 0
        
            Deprecated, for removal: This API element is subject to removal in a future version.
            Penalize a match by the :class:`~org.optaplanner.core.api.domain.constraintweight.ConstraintWeight` negated and
            multiplied with the specific weightMultiplier per score level. Slower than
            :meth:`~org.optaplanner.core.api.score.buildin.hardmediumsoft.HardMediumSoftScoreHolder.penalize`.
        
            Parameters:
                kcontext (org.kie.api.runtime.rule.RuleContext): never null, the magic variable in DRL
                hardWeightMultiplier (int): at least 0
                mediumWeightMultiplier (int): at least 0
                softWeightMultiplier (int): at least 0
        
        
        """
        ...
    @typing.overload
    def penalize(self, ruleContext: org.kie.api.runtime.rule.RuleContext, int: int, int2: int, int3: int) -> None: ...
    @typing.overload
    def penalize(self, ruleContext: org.kie.api.runtime.rule.RuleContext) -> None: ...
    @typing.overload
    def reward(self, ruleContext: org.kie.api.runtime.rule.RuleContext, int: int) -> None:
        """
            Deprecated, for removal: This API element is subject to removal in a future version.
            Reward a match by the :class:`~org.optaplanner.core.api.domain.constraintweight.ConstraintWeight` multiplied with the
            weightMultiplier for all score levels.
        
            Parameters:
                kcontext (org.kie.api.runtime.rule.RuleContext): never null, the magic variable in DRL
                weightMultiplier (int): at least 0
        
            Deprecated, for removal: This API element is subject to removal in a future version.
            Reward a match by the :class:`~org.optaplanner.core.api.domain.constraintweight.ConstraintWeight` multiplied with the
            specific weightMultiplier per score level. Slower than
            :meth:`~org.optaplanner.core.api.score.buildin.hardmediumsoft.HardMediumSoftScoreHolder.reward`.
        
            Parameters:
                kcontext (org.kie.api.runtime.rule.RuleContext): never null, the magic variable in DRL
                hardWeightMultiplier (int): at least 0
                mediumWeightMultiplier (int): at least 0
                softWeightMultiplier (int): at least 0
        
        
        """
        ...
    @typing.overload
    def reward(self, ruleContext: org.kie.api.runtime.rule.RuleContext, int: int, int2: int, int3: int) -> None: ...
    @typing.overload
    def reward(self, ruleContext: org.kie.api.runtime.rule.RuleContext) -> None: ...


class __module_protocol__(typing.Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.optaplanner.core.api.score.buildin.hardmediumsoft")``.

    HardMediumSoftScore: typing.Type[HardMediumSoftScore]
    HardMediumSoftScoreHolder: typing.Type[HardMediumSoftScoreHolder]
